class CreateArticles < ActiveRecord::Migration
  def change
    create_table :articles do |t|
      t.string :title
      t.text :text
      t.integer :author_id
      t.text	:info

      t.timestamps null: false
    end
  end
end
