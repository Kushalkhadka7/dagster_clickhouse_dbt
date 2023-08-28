import os
import subprocess
import urllib.request

from abc import ABC, abstractmethod
from dagster import ConfigurableResource


class APIClient(ConfigurableResource, ABC):
    @abstractmethod
    def download_file(self, url: str, dirName: str, fileName: str):
        pass


class GithubApiClient(APIClient):
    async def download_file(self, url: str, dirName: str, fileName: str):
        current_dir = os.getcwd()
        os.chdir(dirName)

        urllib.request.urlretrieve(url, fileName)

        subprocess.Popen(["unxz", fileName])

        # [NOTE]: Needed if we want the file format to be `.csv`
        # tsv_file_name = ".".join(fileName.split('.')[:-1])

        # # reading given tsv file
        # csv_table=pd.read_table(tsv_file_name,low_memory=False)

        # csv_file_name = fileName.split('.')[0]+'.csv'

        # # converting tsv file into csv
        # csv_table.to_csv(csv_file_name,index=False)

        # os.remove(tsv_file_name)

        os.chdir(current_dir)

        print(f"{fileName} file successfully downloaded.")
