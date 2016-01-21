class Article < ActiveRecord::Base
	#attr_accessor :title ,:text ,:author_id
	validates :title, presence: true,length: { maximum: 255 },uniqueness: true
	validates :text, presence: true	,length:{ maximum: 65535 }
	validates :info, presence: true	,length:{ maximum: 255 }
	belongs_to :author
	has_many :comments
end  