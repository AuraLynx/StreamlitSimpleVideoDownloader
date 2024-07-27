import os
import glob
import streamlit as st
import yt_dlp


def download_video(
        url: str,
        component: st.container,
) -> None:
    output_template = './%(title)s.%(ext)s'
    ytd_opts = {
        'format': 'mp4',
        'outtmpl': output_template,
        'quiet': False,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ytd_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            component.success('ダウンロード成功')
        return filename

    except Exception as e:
        component.error(f'エラーが発生しました: {str(e)}')

def init_app() -> None:
    video_list = glob.glob('*.mp4')
    if len(video_list) > 0:
        for i_file in video_list:
            os.remove(i_file)
            print(f'{i_file} deleted...')
    else:
        pass

def main():
    init_app()
    url_input = st.text_input(
        'URLを1つ入力してね',
        value=None,
    )

    if st.button('Start Download'):
        result_placeholder = st.container()

        if url_input:
            with st.spinner('Downloading...'):
                result_placeholder.write(url_input)
                filename = download_video(
                    url_input,
                    result_placeholder,
                )
            
            with open(filename, "rb") as file:
                st.download_button(
                    label='Download video',
                    data=file,
                    file_name=os.path.basename(filename),
                    mime='video/mp4',
                )
        else:
            st.write("URLが入力されていません")

if __name__ == '__main__':
    main()
