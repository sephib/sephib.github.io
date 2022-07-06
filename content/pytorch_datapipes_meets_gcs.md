Title: When datapipes meets GCS
Date: 2022-07-06  
Author: Sephi Berry  
Tags: python pytorch
Summary: The reality when using pipelines infrastructure
Category: posts pipeline
status: draft


# Background

Working in the ML arena requires smart usage of data, in addition to the flexability of menupelation of data. A common way to do so to use `pipeline`s that allow for a structure framework to mange such processes.
Lately we wanted to run some menupelation using the pytorch framework. Since some of our data is stored on GCP in their buckets (GCS), we thought that it will be able to use [pytorch datapipes](https://pytorch.org/data/main/index.html) as our framework. Of-the-bat it seems simple since the [IO datapipes](https://pytorch.org/data/main/torchdata.datapipes.iter.html#io-datapipes) seems to be comprehansive, however as usual - once the implementation starts we found an crucial issue.

NOTE - discussion on [discuss pytorch]I(https://discuss.pytorch.org/t/using-a-google-cloud-storage-bucket-for-dataset/146253)


# Security - looked over (as usual???) 

As mentioned our data was in a secure GCS bucket. In order to access the data `datapipes` has implemented an [FSSPEC]() (BTW for `S3` there is a dedicated [S3FileListener](https://pytorch.org/data/main/generated/torchdata.datapipes.iter.S3FileLister.html#torchdata.datapipes.iter.S3FileLister))