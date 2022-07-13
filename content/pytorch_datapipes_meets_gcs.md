Title: When Datapipes Meets GCS
Date: 2022-07-06  
Author: Sephi Berry  
Tags: python pytorch GCP
Summary: The reality when using pipelines infrastructure
Category: posts pipeline
<!-- status: draft -->

<a rel="pytorch_gcs_logo"><img src="images/Pytorch_GCS_logo.png" width=700 height=300 /></a>  

# Background

Working in the ML arena requires a smart usage of data, in addition to maximum flexibility while manipulation of datasets. A common way to do so is to use `pipeline`s that allow for a structural manner to manage these processes.  
Lately we wanted to run some image manipulation using the [pytorch framework](https://pytorch.org). Since our data is stored on GCP in their buckets (GCS), we thought that we will be able to use [pytorch datapipes](https://pytorch.org/data/main/index.html) as our pipeline framework. Of-the-bat it seems simple since the [IO datapipes](https://pytorch.org/data/main/torchdata.datapipes.iter.html#io-datapipes) seems to be comprehensive, however as usual - once the implementation starts we found some issue.  

# Our Use Case

We had some images that we needed to convert into embeddings and save them into a bucket. So with the inspiration of [the documented examples](https://pytorch.org/data/main/examples.html) we built our `datapipe` as follows:  

```python
def image_datapipe(root_dir):
    datapipe = FSSpecFileLister(root=root_dir)
    datapipe = datapipe.open_file_by_fsspec(mode="rb")
    datapipe = datapipe.map(PIL_open)
    datapipe = datapipe.map(row_emb_processor)
    datapipe = datapipe.map(post_process)
    datapipe = datapipe.save_by_fsspec(filepath_fn=filepath_fn, mode="wb")
    return datapipe
```  

## Security - looked over (as usual???)


1. `FSSpecFileLister` is an object to access the files in a filesystem.
   1. In order to access the GCS filesystem the pytorch's `open_file_by_fsspec` function uses the library [fsspec](https://filesystem-spec.readthedocs.io/en/latest/) with [following code](https://github.com/pytorch/data/blob/cd38927904836f6f67ce33bfaee094fff4078402/torchdata/datapipes/iter/load/fsspec.py#L128)  

    ```python
    fs, path = fsspec.core.url_to_fs(root, **self.kwargs)
    ```  

   The problem with this function is that it does not take into account the possibility to pass credential for authentication - [see thread on pytorch discuss forum](https://discuss.pytorch.org/t/using-a-google-cloud-storage-bucket-for-dataset/146253)  

   2. In order to solve this issue we wrapped the `fsspec.core.url_to_fs` function into an internal function, while using the   

```python  
def _url_to_fs(root, token, **self.kwargs):  
    fs, path = fsspec.core.url_to_fs(root, token=token_path, **self.kwargs)  
    # hotfix - since the GCS fsspec implementation can return ('gcs', 'gs') as protocol
    if isinstance(fs.protocol, Tuple) and len(fs.protocol) > 1:  
        fs.protocol = fs.protocol[1]  
    return fs, path  
``` 


* BTW for `AWS S3` there is a dedicated [S3FileListener handler](https://pytorch.org/data/main/generated/torchdata.datapipes.iter.S3FileLister.html#torchdata.datapipes.iter.S3FileLister)

## Now for the rest of the pipeline

2. Now we can add to our pipeline additional functionality.  
    First we will open our image as a stream using `PIL.Image`:  

```python
def PIL_open(data):
    return (
        path_name=data[0],
        file_stream=Image.open(gfs.open(data[0]))
        )
```

* the `gfs` is using the implementation of `fsspec` for GCS - [gcsfs](https://gcsfs.readthedocs.io/en/latest/)


3. In the next step we will create embeddings from our image stream. We used a wrapped [CLIP model](https://github.com/openai/CLIP) (`image_processor`). This is always a good practice in order to allow for the possibility to replace the model in the future.  

```python
def row_emb_processor(data):
    data[1] = image_processor.embed(data[1])
    data[1] = data[1].squeeze().numpy().tolist()
    return data
```

4. Since we want to save the embeddings in a `parquet` format, we will use the `post_process` step for this purpose, while allowing to consume the embeddings as `pandas dataframe`s.  

```python
def post_process(data):
    df = pd.DataFrame([[data[1]]], 
                    index=[data[0]], 
                    columns=["emb_CLIP"],
    )
return (data, df.to_parquet())
```  

5. Lastly, on our final step we will use the `save_by_fsspec` method to save the embeddings back into a GCS bucket. Since we already fixed the `url_to_fs` accessing the bucket is straight forward. All we need is to supply the target name of the file.  

```python
def filepath_fn(data):
    return f"gs://bucket/folder/asset_{data[0]}.parq"
```

# Additional Thoughts

* Moving the data between the various pipe steps can be easier when defining a `dataclass` object - thus easily referencing the required property of the image in the various stages.  
e.g. instead of calling `data[1]` for the embedding - way not use *`data.file_stream`*. Hopefully this will be elaborated in a different post.



# Summary

As a strong advocate for embracing *pipelines* where ever we can, the implementation of the various stages can be challenging. There is no place to accumulate any technical debt in the security realm - thus solving the secure access between `pytorch datapipes`  and `gcs` will allow for reuse and agility in future projects. 