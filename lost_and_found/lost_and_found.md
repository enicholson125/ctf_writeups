# Lost and Found

This was in the cloud section and was a service account key json.

The first thing I did after downloading the json was to have a look at it, which told me the name of the project it was associated with. I could then authenticate with gcloud as that service account and configure that project.
```
gcloud config set project ductf-lost-n-found
gcloud auth activate-service-account --key-file legacy.json
```

This meant that I could use gcloud to have a poke around the resources in the project that the service account had access to. Most of the APIs in the project weren't enabled, but the Google Secrets one was, and the service account had access. I listed the secrets present in the project:
```
gcloud secrets list
```
which revealed a secret called `unused_data`. I then listed the versions of the secret. There was only one version so I downloaded that. It was base64 encoded so I decoded it and read it into a local file:
```
gcloud secrets versions list unused_data
gcloud secrets versions access 1 --secret=unused_data | base64 --decode > output
```

I had a look at the output but it was a binary, not a flag. It's good practice to encrypt secrets, so I wondered if potentially this secret was encrypted with a Google KMS key. I listed the KMS keyrings and keys available in the project, making a guess that an Australian CTF would be using Australian regions:
```
gcloud kms keyrings list --location australia-southeast1 # nothing
gcloud kms keyrings list --location australia-southeast2 # a keyring called wardens-locks
gcloud kms keys list --location australia-southeast2 --keyring wardens-locks
```
Listing the keys on the keyring revealed 10 or so keys associated with it. There wasn't an obvious key to try first so I went through them all, attempting to decrypt the secret I'd found with them:
```
gcloud kms decrypt --ciphertext-file output --plaintext-file flag --location australia-southeast2 --keyring wardens-locks --key a-silver-key
```
Eventually I found the right key and got the flag!
