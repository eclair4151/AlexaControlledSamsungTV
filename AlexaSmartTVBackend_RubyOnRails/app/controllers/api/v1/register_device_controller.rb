require 'openssl'
require 'aws-sdk-iot'

class Api::V1::RegisterDeviceController < ApiController
    
    
    def create
        if params[:uuid]
            device =  @user.devices.find_by_uuid!(params[:uuid])
            private_key =  device.private_key
            pubic_certificate =  device.pubic_certificate
            uuid = device.uuid
            device.name = params[:name]
            device.user_id = @data[0]['user_id'] 
            device.save
        else
            uuid = SecureRandom.uuid
            
            Aws.config.update({
                region: 'us-east-1',
                credentials: Aws::Credentials.new('[YOUR_AWS_ACCESS_KEY]', '[YOUR_AWS_SECRET]')
            })
            
            root_ca = OpenSSL::X509::Certificate.new File.read(File.join(Rails.root, 'app','certs','rootcert.pem'))
            root_key = OpenSSL::PKey::RSA.new  File.read(File.join(Rails.root, 'app','certs','rootcert.key'))
            
            device_key = OpenSSL::PKey::RSA.new 2048
            cert = OpenSSL::X509::Certificate.new
            cert.version = 2
            cert.serial = 2
            cert.subject = OpenSSL::X509::Name.parse "/DC=org/DC=ruby-lang/CN=Ruby certificate"
            cert.issuer = root_ca.subject # root CA is the issuer
            cert.public_key = device_key.public_key
            cert.not_before = Time.now
            cert.not_after = cert.not_before + 5000 * 365 * 24 * 60 * 60 # 5000 years validity. Can never be too careful... (im to lazy to implement reauth)
            ef = OpenSSL::X509::ExtensionFactory.new
            ef.subject_certificate = cert
            ef.issuer_certificate = root_ca
            cert.add_extension(ef.create_extension("keyUsage","digitalSignature", true))
            cert.add_extension(ef.create_extension("subjectKeyIdentifier","hash",false))
            cert.sign(root_key, OpenSSL::Digest::SHA256.new)
            device_and_CA = cert.to_s + root_ca.to_s
            
            iot_client = Aws::IoT::Client.new
            cert_resp = iot_client.register_certificate({
                                       certificate_pem: cert.to_s, 
                                       set_as_active: root_ca.to_s,
                                       status: "ACTIVE",
                                   })
            
            policy = "{
              \"Version\": \"2012-10-17\",
              \"Statement\": [
                {
                  \"Effect\": \"Allow\",
                  \"Action\": \"iot:Connect\",
                  \"Resource\": \"arn:aws:iot:us-east-1:141651249291:client\/#{uuid}\"
                },
                {
                  \"Effect\": \"Allow\",
                  \"Action\": \"iot:Subscribe\",
                  \"Resource\": \"arn:aws:iot:us-east-1:141651249291:topicfilter\/power\/#{uuid}\"
                },
                {
                  \"Effect\": \"Allow\",
                  \"Action\": \"iot:Receive\",
                  \"Resource\": \"arn:aws:iot:us-east-1:141651249291:topic\/power\/#{uuid}\"
                },
                {
                  \"Effect\": \"Allow\",
                  \"Action\": \"iot:Subscribe\",
                  \"Resource\": \"arn:aws:iot:us-east-1:141651249291:topicfilter\/channel\/#{uuid}\"
                },
                {
                  \"Effect\": \"Allow\",
                  \"Action\": \"iot:Receive\",
                  \"Resource\": \"arn:aws:iot:us-east-1:141651249291:topic\/channel\/#{uuid}\"
                },
                {
                  \"Effect\": \"Allow\",
                  \"Action\": \"iot:Subscribe\",
                  \"Resource\": \"arn:aws:iot:us-east-1:141651249291:topicfilter\/speaker\/#{uuid}\"
                },
                {
                  \"Effect\": \"Allow\",
                  \"Action\": \"iot:Receive\",
                  \"Resource\": \"arn:aws:iot:us-east-1:141651249291:topic\/speaker\/#{uuid}\"
                },
                {
                  \"Effect\": \"Allow\",
                  \"Action\": \"iot:Subscribe\",
                  \"Resource\": \"arn:aws:iot:us-east-1:141651249291:topicfilter\/playback\/#{uuid}\"
                },
                {
                  \"Effect\": \"Allow\",
                  \"Action\": \"iot:Receive\",
                  \"Resource\": \"arn:aws:iot:us-east-1:141651249291:topic\/playback\/#{uuid}\"
                }
              ]
            }"
            
            policy_name = uuid + '_policy'
            
            policy_resp = iot_client.create_policy({
              policy_name: policy_name,
              policy_document: policy
            })
            
            
            attach_resp = iot_client.attach_principal_policy({
              policy_name: policy_name, # required
              principal: cert_resp.certificate_arn  # required
            })
            
            private_key =  device_key.to_s
            pubic_certificate =  device_and_CA
            
            device = @user.devices.create!(uuid: uuid, private_key: private_key, pubic_certificate: pubic_certificate, name: params[:name], last_pinged: Time.now())
        end
        
        device.tvs.delete_all
        
        params[:tvs].each{|tv|
          device.tvs.create!(name: tv[:name], mac_address: tv[:mac_address])
        }
        
        render json: {uuid: uuid, private_key: private_key, pubic_certificate: pubic_certificate}
    end
    
end
