def get_file_upload_path(path_url, path_vars_array):
	return path_url.format(path_vars_array)

def recipe_image_path(instance, filename):
    url = "recipes/{0[0]}_{0[1]}_{0[2]}"
    vars_array = [
        instance.recipe_name,
        instance._id,
        filename
    ]
    return get_file_upload_path(url, vars_array)