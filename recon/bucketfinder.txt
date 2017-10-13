public = """
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
	<Name>digipublic</Name>
	<Prefix></Prefix>
	<Marker></Marker>
	<MaxKeys>1000</MaxKeys>
	<IsTruncated>false</IsTruncated>
</ListBucketResult>
"""

private = """
<Error>
	<Code>AccessDenied</Code>
	<Message>Access Denied</Message>
	<RequestId>7F3987394757439B</RequestId>
	<HostId>kyMIhkpoWafjruFFairkfim383jtznAnwiyKSTxv7+/CIHqMBcqrXV2gr+EuALUp</HostId>
</Error>
"""

notfound = """
<Error>
    <Code>NoSuchBucket</Code>
    <Message>The specified bucket does not exist</Message>
    <BucketName>publicdesk</BucketName>
    <RequestId>E297102A871CF5ED</RequestId>
    <HostId>
XYVXa90dZ34B9BsuP7QcaZCM9RDcKbjJYIa/bs7LuBXBG08MDOOBRr1/YcPEnk/BO/sNdIDdguM=
    </HostId>
</Error>
"""


