class CreateComments < ActiveRecord::Migration
  def change
    create_table :comments do |t|
      t.integer :article_id
      t.text :text
      t.integer :author_id

      t.timestamps null: false
    end
  end
end
