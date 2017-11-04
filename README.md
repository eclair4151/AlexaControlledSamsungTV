how to register certs


openssl genrsa -out deviceCert.key 2048
openssl req -new -key deviceCert.key -out deviceCert.csr
openssl x509 -req -in deviceCert.csr -CA sampleCACertificate.pem -CAkey sampleCACertificate.key -CAcreateserial -out deviceCert.crt -days 99999 -sha256

cat deviceCert.crt sampleCACertificate.pem > deviceCertAndCACert.crt

register deviceandcert thing
http://docs.aws.amazon.com/cli/latest/reference/iot/register-certificate.html
https://docs.aws.amazon.com/iot/latest/apireference/API_RegisterCertificate.html

create policy
http://docs.aws.amazon.com/cli/latest/reference/iam/create-policy.html
https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreatePolicy.html


attach policy to arn
http://docs.aws.amazon.com/cli/latest/reference/iot/attach-principal-policy.html
https://docs.aws.amazon.com/iot/latest/apireference/API_AttachPrincipalPolicy.html


 mosquitto_pub --cafile root.cert --cert deviceCertAndCACert.crt --key deviceCert.key
 file names ^