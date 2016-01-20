class AuthorsController < ApplicationController
	def index
		@authors = Author.all
	end
	def search_friends
    @authors = Author.where("name like ?","%"+params[:keywords]+"%")
    #render 'all'
  	end
	def show
		@author = Author.find(params[:id])
		@author.articles = @author.articles.limit(10);
		@author.comments = @author.comments.limit(10);
		@recommend_articles = Article.where(info:@author.info).limit(10);
	end
	def new
		@author = Author.new
	end
	def create
		params.permit!
		@author = Author.new(params[:author])
		if @author.save
			log_in @author
			redirect_to @author
		else
		render 'new'
		end
	end
	def edit
		@author = Author.find(params[:id])
	end
	def update
		@author = Author.find(params[:id])
    @author.update_attributes(author_params)
    @author.articles = @author.articles.limit(10);
    @author.comments = @author.comments.limit(10);
    @recommend_articles = Article.where(info:@author.info).limit(10);
		render 'show'
	end

	private

	def author_params
		params.require(:author).permit(:name, :email, :password,
		:password_confirmation,:info)
	end
end
