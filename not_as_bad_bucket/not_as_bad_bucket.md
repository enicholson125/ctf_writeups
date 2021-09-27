# Not As Bad Bucket

This was in the cloud section and was a link to a blob in a Google Storage bucket: https://storage.googleapis.com/ductf-not-as-bad-ductf/index.html.

Clicking on the link revealed that anonymous users did not have access to the blob. I then had a look to see if list permissions on the bucket were available to anonymous users by taking the index.html off the link: https://storage.googleapis.com/ductf-not-as-bad-ductf/. Anonymous users didn't have bucket list permissions either.

The word anonymous reminded me of a feature in Google Storage buckets. You can set permissions to be available to all users (anonymous access), specific users or to be available to all *authenticated* users, i.e. everyone with a Google account.

I turned to gcloud and gsutil at this point:
```
gcloud auth login # Make sure I'm logged in
gsutil ls gs://ductf-not-as-bad-ductf # List the bucket
```
Listing the bucket worked! It revealed a `pics` directory which contained a `flag.txt` file.
```
gsutil cp gs://ductf-not-as-bad-ductf/pics/flag.txt .
```
and I had the flag.
