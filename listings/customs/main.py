from .getListingData import UrlFetcher
from .formatData import FormatData
from .uploadListing import AddListing

test = UrlFetcher()
convert = FormatData()
uploader = AddListing()


def upload(ids, token):
    for singleId in ids:
        data = test.fetch_data(singleId)

        convertedData = convert.convert_to_upload_format(data, '568625279')

        uploader.setHeaders(token)

        print(uploader.data(convertedData))
