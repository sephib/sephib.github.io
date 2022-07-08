Title: When datapipes meets GCS
Date: 2022-07-06  
Author: Sephi Berry  
Tags: python pytorch
Summary: The reality when using pipelines infrastructure
Category: posts pipeline
status: draft


# Background

Working in the ML arena requires smart usage of data, in addition to the flexibility of manipulation of data. A common way to do so to use `pipeline`s that allow for a structure framework to mange such processes.  
Lately we wanted to run some manipulation using the [pytorch framework](https://pytorch.org). Since some of our data is stored on GCP in their buckets (GCS), we thought that we will be able to use [pytorch datapipes](https://pytorch.org/data/main/index.html) as our framework. Of-the-bat it seems simple since the [IO datapipes](https://pytorch.org/data/main/torchdata.datapipes.iter.html#io-datapipes) seems to be comprehensive, however as usual - once the implementation starts we found some challenging issue.



# Our Use Case
We had some images that we needed to convert into embeddings - so with the inspiration of [examples](https://pytorch.org/data/main/examples.html) we build our `datapipe` as follows:  
```python
def build_image_datapipes(root_dir):
    datapipe = FSSpecFileLister(root=root_dir)
    datapipe = datapipe.open_file_by_fsspec(mode="rb")
    datapipe = datapipe.map(PIL_open)
    datapipe = datapipe.map(row_emb_processor)
    datapipe = datapipe.map(post_process)
    datapipe = datapipe.save_by_fsspec(filepath_fn=filepath_fn, mode="wb")
    return datapipe
```  

### Break it down 

1. `FSSpecFileLister` is an object to access the files
   1. In order to access the filesystem  the pytorch's `open_file_by_fsspec` function uses the [following code](https://github.com/pytorch/data/blob/d19858202df7e8b75765074259e6023f539cbf3f/torchdata/datapipes/iter/load/fsspec.py#L74)  
    ```python
    fs, path = fsspec.core.url_to_fs(root, **self.kwargs)
    ```
   The problem with this function is that it does not take into account the possibility to pass credential for authentication - [see link on pytorch discuss forum](https://discuss.pytorch.org/t/using-a-google-cloud-storage-bucket-for-dataset/146253)  
   
   1. In order to solve this issue we wrapped the function into an internal function
    ```python
    def _url_to_fs(root, token, **self.kwargs)
        fs, path = fsspec.core.url_to_fs(root, token=token_path, **self.kwargs)
        # hotfix - since the GCS fsspec implementation can return ('gcs', 'gs') as protocol
        if isinstance(fs.protocol, Tuple) and len(fs.protocol) > 1:
            fs.protocol = fs.protocol[1]
        return fs, path
    ```  

2.  Now we can add to our pipeline additional functionality.      
    First we will open our image as a stream using `PIL.Image`:
    ```python
    def PIL_open(data):
        return (
            path_name=data[0],
            file_stream=Image.open(fs.open(data[0]))
            )
    )
    ```

3. In the next step we will create embeddings from our image stream. We used a wrapped [CLIP model](https://github.com/openai/CLIP).
    ```python
    def row_emb_processor(data):
        data[1] = image_processor.embed(data[1])
        data[1] = data[1].squeeze().numpy().tolist()
        return data
    ```
4. Since we want to save the embeddings in a `parquet` format, we will use the `post_process` step to convert it, while allowing to consume the embeddings as `pandas dataframe`s.
    ```python
    def post_process(data):
        df = pd.DataFrame([[data[1]]], 
                    index=[data[0]], 
                    columns=["emb_CLIP"],
        )
    return (data, df.to_parquet())
    ```
5.  Finally on our final step we will use the `save_by_fsspec` method to save the embeddings back into a GCS bucket. Since we already fixed the `url_to_fs` accessing the bucket is strait forward. All we need is to supply the target name of the file.
    ```python
    def filepath_fn(data):
        return f"gs://destination/bucket/asset_{data[0]}.parq"
    ```
6.   



## The simple of

# Security - looked over (as usual???) 

As mentioned our data was in a secure GCS bucket. In order to access the data `datapipes` has implemented an [FSSPEC]() to access files from file systems.  

(BTW for `S3` there is a dedicated [S3FileListener](https://pytorch.org/data/main/generated/torchdata.datapipes.iter.S3FileLister.html#torchdata.datapipes.iter.S3FileLister))

Building [fsspec.core.url_to_fs](https://github.com/pytorch/data/blob/cd38927904836f6f67ce33bfaee094fff4078402/torchdata/datapipes/iter/load/fsspec.py#L128)


# Additional Thoughts
* Moving the data between the various pipe steps can be easier when defining a `dataclass` object - thus easily referencing the required property of the image in the various stages.
e.g. instead of calling `data[1]` for the embedding - way not use *`data.file_stream`*. Hopefully will be elaborated in a different post.

# Summary