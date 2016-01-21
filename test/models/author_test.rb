require '../test_helper'

class AuthorTest < ActiveSupport::TestCase
    test "email address should not be saved without @" do
    mixed_case_email = "Moon"
    @user.email = mixed_case_email
    @user.save
    assert_not_equal mixed_case_email.downcase,@user.reload.email
  end
end
