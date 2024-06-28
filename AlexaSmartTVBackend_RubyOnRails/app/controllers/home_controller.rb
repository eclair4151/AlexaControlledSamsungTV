class HomeController < ApplicationController
  def index
    @devices = @user.devices.where(:deleted => false).order(:created_at)
  end
  
  
  def delete
    device = @user.devices.find_by_uuid!(params[:id])
    device.deleted = true
    device.save
    redirect_to '/'
  end
  
end
