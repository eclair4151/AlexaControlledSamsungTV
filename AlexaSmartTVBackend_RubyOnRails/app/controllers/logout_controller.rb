class LogoutController < ApplicationController
skip_before_action :authenticate_user

  def index
    cookies.delete :jwt
    redirect_to '/login'
  end
end