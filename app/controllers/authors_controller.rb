class AuthorsController < ApplicationController
	def index
		@authors = Author.all
	end
	def show
		@author = Author.find(params[:id])
	end
	def new
		@author = Author.new
	end
	def create
		params.permit!
		@author = Author.new(params[:author])
		if @author.save
			log_in @author
			flash[:success] = "欢迎来到果壳Today!"
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
		flash[:success] = "数据已更新"
		render 'show'
	end

	private

	def author_params
		params.require(:author).permit(:name, :email, :password,
		:password_confirmation,:info)
	end
end
