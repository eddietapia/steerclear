import httplib, urllib, base64
import json

def is_celebrity(image):
    headers = {
        # Request headers.
        'Content-Type': 'application/octet-stream',

        # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
        'Ocp-Apim-Subscription-Key': '03fbba8f7bf047afad169890d29059b5',
    }

    params = urllib.urlencode({
        # Request parameters. All of them are optional.
        'visualFeatures': 'Categories',
        'details': 'Celebrities',
        'language': 'en',
    })

    # Replace the three dots below with the URL of a JPEG image of a celebrity.
    #body = "{'url':'http://shpe.ucsd.edu/assets/images/team/Eddie_T.jpg'}"
    #body = "{'url':'http://gazettereview.com/wp-content/uploads/2016/05/David-Beckham.jpg'}"
    body = "{'url':'http://cdn.playbuzz.com/cdn/6b4354e7-d674-4a44-8150-215c27035f1c/202c8f4a-410f-4b6e-8e07-273ceaf5078d.jpeg'}"


    try:
        # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the 
        #   URL below with "westus".
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, image, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        data = json.loads(data)
        #celeb_name = data['categories'][0]['detail']['celebrities'][0]['name']
	print data
        a= data['categories'][0]['detail']
        if len(a) == 0:
            print a
            return a
        else:
            a = a['celebrities'][0]
            if len(a) == 0:
                print a
                return a
            print a['name']
            return a['name']
        return a
    
    except Exception as e:
        #print("[Errno {0}] {1}".format(e.errno, e.strerror))
        print "Error in analyze."

