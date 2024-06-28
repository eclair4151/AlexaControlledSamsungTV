class PrivacyController < ApplicationController
  skip_before_action :authenticate_user
  layout 'root'


  def index
  end
  
  
  
end
