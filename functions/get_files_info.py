import os




def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'


        dir_list = []
        for dir_name in os.listdir(target_dir):
            dir_path = os.path.join(target_dir, dir_name)
            size = os.path.getsize(dir_path)
            dir_list.append(
                f'- {dir_name}: file_size={size} bytes, is_dir={os.path.isdir(dir_path)}'
            )
        return "\n".join(dir_list)
    except Exception as e:
        return f'Error: {str(e)}'
        