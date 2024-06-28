Rails.application.routes.draw do
  
  get 'alexa_login/index'

  get 'profile/index'

  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".
  mount LetsencryptPlugin::Engine, at: '/'
  
  root 'home#index'
  match 'login', to: 'login#index', :via => 'get'
  match 'login', to: 'login#create', :via => 'post'
  match 'alexa_login', to: 'alexa_login#index', :via => 'get'
  match 'alexa_login', to: 'alexa_login#create', :via => 'post'
  match 'choose_device', to: 'choose_device#index', :via => 'get'
  match 'choose_device', to: 'choose_device#create', :via => 'post'

  match 'logout', to: 'logout#index', :via => 'get'

  match 'create_account', to: 'create_account#index', :via => 'get'
  match 'create_account', to: 'create_account#create', :via => 'post'
  match 'forgot_password', to: 'forgot_password#create', :via => 'post'
  match 'forgot_password', to: 'forgot_password#index', :via => 'get'

  match 'profile', to: 'profile#create', :via => 'post'

  match 'tutorial', to: 'tutorial#index', :via => 'get'
  match 'profile', to: 'profile#index', :via => 'get'
  match 'privacy', to: 'privacy#index', :via => 'get'

  match '/', to: 'home#delete', :via => 'delete'

  
   namespace :api,  :defaults => {:format => :json} do
    namespace :v1 do
      match '/login', to: 'login#create' , :via => 'post'
      match '/auth_token', to: 'auth_token#create', :via => 'post'
      match '/register_device', to: 'register_device#create' , :via => 'post'
      match '/ping', to: 'ping#create' , :via => 'post'
      match '/get_devices', to: 'get_devices#create' , :via => 'post'

    end
  end
  
  
end
