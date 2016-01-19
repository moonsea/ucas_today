class AddRememberDigestToAuthors < ActiveRecord::Migration
  def change
    add_column :authors, :remember_digest, :string
  end
end
