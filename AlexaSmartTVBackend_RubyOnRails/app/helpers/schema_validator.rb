class SchemaValidator

  @@schemas = {
  'login':
      {
        :type => 'object',
        :required => ['email','password'],
        :properties => {
            :email => {:type => 'string'},
            :password => {:type => 'string'}
        }
      },
    'register_device':
      {
        :type => 'object',
        :required => ['name','tvs'],
        :properties => {
            :name => {:type => 'string'},
            :tvs => {:type => 'array',
              'items':{
                :type => 'object',
                :required => ['name','mac_address'],
                :properties => {
                    :name => {:type => 'string'},
                    :mac_address => {:type => 'string'}
                }
              }
            },
            :uuid => {:type => 'string'}
        }
      },
    'ping':
      {
        :type => 'object',
        :required => ['uuid'],
        :properties => {
            :uuid => {:type => 'string'}
        }
      },
      'get_devices':
      {
        :type => 'object',
        :required => ['uuid'],
        :properties => {
            :uuid => {:type => 'string'}
        }
      },
      'auth_token':
      {
        :type => 'object',
        :required => ['code'],
        :properties => {
            :code => {:type => 'string'},
            :grant_type => {:type => 'string'},
            :redirect_uri => {:type => 'string'},
            :client_id => {:type => 'string'}
        }
      }
    
  }

  def self.get_schema(route)
    @@schemas[route.to_sym]
  end
end