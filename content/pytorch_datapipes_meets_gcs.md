Title: When Pytorch Datapipes Meets GCS
Date: 2022-07-06  
Author: Sephi Berry  
Tags: python pytorch GCP
Summary: The reality when using pipeline infrastructure
Category: posts pipeline
<!-- status: draft -->

<a rel="pytorch_gcs_logo"><img src="images/Pytorch_GCS_logo.png" width=700 height=300 /></a>  

# Background

Working in the ML arena requires optimal usage of data, in addition to maximum flexibility while manipulating of datasets. A common way to do so is to use `pipeline`s that allow for a structural framework to manage these processes.  

Lately at  <a rel="Artlist logo" href="https://artlist.io"><img src="images/Artlist Logo 64px.png" height=20 /></a>   we  wanted to run some image manipulations using the [pytorch framework](https://pytorch.org). Since our data are stored in Google Cloud Storage (GCS), we thought that we would be able to use [pytorch datapipes](https://pytorch.org/data/main/index.html) as our pipeline framework.  Of-the-bat it seem simple since the [IO datapipes](https://pytorch.org/data/main/torchdata.datapipes.iter.html#io-datapipes) seems to be comprehensive, however, as usual and to be expected - once the implementation started we were challenged with some technical issues.  

# Our Use Case

We had some images that we needed to convert into embeddings and save them into a bucket. With the inspiration and stimulus of [the documented examples](https://pytorch.org/data/main/examples.html) we built our `pytorch datapipe` as follows:  

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

Lets go over the various steps in the pipeline.

## Who care's about security

`FSSpecFileLister` is an object responsible for accessing the files in a filesystem.

In order to access the `GCS` filesystem, Pytorch's `open_file_by_fsspec` function uses the  [fsspec](https://filesystem-spec.readthedocs.io/en/latest/) library with [following code](https://github.com/pytorch/data/blob/cd38927904836f6f67ce33bfaee094fff4078402/torchdata/datapipes/iter/load/fsspec.py#L128)  

```python
fs, path = fsspec.core.url_to_fs(root, **self.kwargs)
```  

- The problem with this function is that it does not take into account the option to access secured buckets, i.e. how to pass credential for authentication in order to access private buckets - [see thread on pytorch discuss forum](https://discuss.pytorch.org/t/using-a-google-cloud-storage-bucket-for-dataset/146253).

In order to solve this issue we wrapped the `fsspec.core.url_to_fs` function into an internal function, while introducing the option to supply the `credential token`.

```python  
def _url_to_fs(root, token, **self.kwargs):  
    fs, path = fsspec.core.url_to_fs(root, token=token_path, **self.kwargs)  
    # hotfix - since the GCS fsspec implementation can return ('gcs', 'gs') as protocol
    if isinstance(fs.protocol, Tuple) and len(fs.protocol) > 1:  
        fs.protocol = fs.protocol[1]  
    return fs, path  
```

- BTW for `AWS S3` there is a dedicated [S3FileListener handler](https://pytorch.org/data/main/generated/torchdata.datapipes.iter.S3FileLister.html#torchdata.datapipes.iter.S3FileLister)

## Now for the rest of the pipeline

- Now we can add to our pipeline additional functionality.  
    First we will open our image as a stream using `PIL.Image`:  

```python
def PIL_open(data):
    return (
        path_name=data[0],
        file_stream=Image.open(gfs.open(data[0]))
        )
```

The `gfs` is using the implementation of `fsspec` for GCS - [gcsfs](https://gcsfs.readthedocs.io/en/latest/)


- In the next step we will create embeddings from our image stream. We used a wrapped [CLIP model](https://github.com/openai/CLIP) (`image_processor`). Note: it is always good practice to wrap modular functionality in order to allow for future replacement with a new model version.  

```python
def row_emb_processor(data):
    data[1] = image_processor.embed(data[1])
    data[1] = data[1].squeeze().numpy().tolist()
    return data
```

- Since we want to save the embeddings in a `parquet` format, we will use the `post_process` step for this purpose, while allowing to consume the embeddings as `pandas dataframe`s.  

```python
def post_process(data):
    df = pd.DataFrame([[data[1]]], 
                    index=[data[0]], 
                    columns=["emb_CLIP"],
    )
return (data, df.to_parquet())
```  

- Lastly, in our final step we will use the `save_by_fsspec` method to save the embeddings back into a GCS bucket. Since we already fixed the `url_to_fs` accessing the bucket is straight forward. All we need is to supply the target name of the file.  

```python
def filepath_fn(data):
    return f"gs://bucket/folder/asset_{data[0]}.parq"
```

# Additional Thoughts

- Moving the data between the various pipe steps can be made easier when defining a `dataclass` object - by simply referencing the required property of the image in the various stages.  
e.g. instead of calling `data[1]` for the embedding - way not use *`data.file_stream`*. Hopefully this will be elaborated in a different post.

- The issue of accessing the bucket securely has been addressed in [this issue](https://github.com/pytorch/data/issues/497).

# Summary

As a strong advocate for embracing *pipelines* whenever possible, the implementation of the various pipeline stages can be challenging.  

There is no place to accumulate any technical debt in the security realm - thus solving the secure access between `pytorch datapipe`s  and `GCS` will allow for code reuse and agility in future projects.
