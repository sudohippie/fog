__author__ = 'Raghav Sidhanti'

from fog.device import GoogleDrive


class GoogleDriveTest(object):

    @staticmethod
    def test_download():
        drive = GoogleDrive()
        drive.open()
        #c = drive.download(src='/FogTestDoc.txt', dst='/tmp/FogTestDoc.txt')
        c = drive.download(src='/HelloWorld.txt', dst='/tmp/HelloWorld.txt')
        #c = drive.download(src='/sudhi_indiagifts_list')
        drive.close()


if __name__ == '__main__':
    GoogleDriveTest.test_download()
