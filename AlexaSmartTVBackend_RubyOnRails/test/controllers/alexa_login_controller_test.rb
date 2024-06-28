require 'test_helper'

class AlexaLoginControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get alexa_login_index_url
    assert_response :success
  end

end
