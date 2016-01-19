require 'test_helper'
class AuthorTest < ActiveSupport::TestCase
	def setup
		@author = Author.new(name: "Example User", email: "user@example.com",password: "foobar", password_confirmation: "foobar")
	end
	test "should be valid" do
		assert @author.valid?
	end

	test "name should be present" do
		@author.name = " "
		assert_not @author.valid?
	end

	test "email should be present" do
		@author.email = " "
		assert_not @author.valid?
	end

	test "name should not be too long" do
		@author.name = "a" * 51
		assert_not @author.valid?
	end

	test "email should not be too long" do
		@author.email = "a" * 256
		assert_not @author.valid
	end
	test "password should have a minimum length" do
		@author.password = @uauthor.password_confirmation = "a" * 5
		assert_not @user.valid?
	end
end

