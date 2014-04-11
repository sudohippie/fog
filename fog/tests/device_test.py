__author__ = 'Raghav Sidhanti'

from fog.device import GoogleDrive


class GoogleDriveTest(object):

    @staticmethod
    def test_download():
        drive = GoogleDrive()
        drive.open()
        #c = drive.download(src='/FogTestDoc.txt', dst='/tmp/FogTestDoc.txt')
        c = drive.download(src='tmp/', dst='/tmp/var/')
        #c = drive.download(src='/sudhi_indiagifts_list')
        drive.close()

    @staticmethod
    def test_delete():
        drive = GoogleDrive()
        drive.open()
        drive.delete(src='/tmp/HelloWod.txt')
        drive.close()


if __name__ == '__main__':
    GoogleDriveTest.test_delete()
