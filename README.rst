sxclient: Python SX client-side library
=======================================

Introduction
------------

sxclient is a library which implements client-side methods for communicating
with an SX Cluster. Using the provided objects and functions, it is possible to
prepare and send a query as per the API documentation at
http://docs.skylable.com/.

Internally, sxclient uses requests library (http://python-requests.org/) and
currently requires Python 2.7.


Usage
-----

In order to run an operation provided by the library, you must:

- prepare a Cluster object, containing cluster location data;
- prepare a UserData object, containing user credentials used to authorize
  operations;
- prepare either a ClusterSession object or SXController object which serves as
  a context for the connections with the cluster.

Afterwards, you can run a series of operations using the previously created
ClusterSession object as a context.


Initializing Cluster object
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The most basic way of initializing the Cluster object is to pass the cluster
name:

::

   cluster = sxclient.Cluster('my.cluster.example.com')

If the passed name is not a FQDN, you should pass an IP address too. It will be
used to communicate with the cluster in place of name.

::

   cluster = sxclient.Cluster('clustername', ip_addresses='127.0.0.1')

You can also pass a list of IP addresses.

::

   cluster = sxclient.Cluster('clustername', ip_addresses=['127.0.0.1','127.0.0.2','127.0.0.3'])

In case you don't want the connection to be secured by SSL, set ``is_secure``
to ``False``:

::

   cluster = sxclient.Cluster('my.cluster.example.com', is_secure=False)

You can also pass a custom port number:

::

   cluster = sxclient.Cluster('my.cluster.example.com', port=8000)

In order to use a custom CA certificate for verification, pass a path to CA
bundle in ``verify_ssl_cert`` parameter:

::

   cluster = sxclient.Cluster('my.cluster.example.com', verify_ssl_cert='/path/to/ca/bundle')

In case you don't want to verify SSL certificates at all, set
``verify_ssl_cert`` to ``False``.


Initializing UserData object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are multiple initialization methods for UserData. You can provide a path
to the key file:

::

   user_data = sxclient.UserData.from_key_path('/path/to/keyfile')

The key itself can be provided too — either encoded in base64:

::

   user_data = sxclient.UserData.from_key('ZP1rHyR0QB6zEvCwYexGl9SF1G143C/D2hG9rEisLL2zJV3kWQvtAwAA')

or in its binary form:

::

   user_data = sxclient.UserData('d\xfdk\x1f$t@\x1e\xb3\x12\xf0\xb0a\xecF\x97\xd4\x85\xd4mx\xdc/\xc3\xda\x11\xbd\xacH\xac,\xbd\xb3%]\xe4Y\x0b\xed\x03\x00\x00')

You can also initialize the object with username and password (and cluster
UUID):

::

   user_data = sxclient.UserData.from_userpass_pair('a_user', 'a_password', '10ca10ca-10ca-10ca-10ca-10ca10ca10ca')


Initializing and working with SXController
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After preparing Cluster and UserData objects you may create an SXController object:

::

   sx = sxclient.SXController(cluster, user_data)

Then get all available operations from 

::

   print sx.available_operations

You may call any operation via

::

   sx.listUsers.call(...)

The return value is a HTTP response object holding the response from SX server. 
If a command supports the JSON format (as most of them do) you may call it directly:

::

   sx.listUsers.json_call(...)

After you are done working with SXController gracefully close it with:

::

   sx.close()


High level operations
^^^^^^^^^^^^^^^^^^^^^

Uploading and downloading files using the aforementioned operations requires 
some low level knowledge of the underlying SX protocol.
To make your life easier, we added three dedicated helpers.

For a given SXController if you wish to upload a file use:

::

   import os
   file_size = os.stat('myfile.txt').st_size
   uploader = sxclient.SXFileUploader(sx)
   with open('myfile.txt', 'r') as fo:
      uploader.upload_stream('my-volume', file_size, 'my_new_file_name.txt', fo)

and if you wish to download a file use:

::

   with sxclient.SXFileDownloader(sx) as downloader:
      content = downloader.get_file_content('my-volume', 'my_new_file_name.txt')

There is another downloader available called SXFileCat. You can use it like this:

::

   downloader = sxclient.SXFileCat(sx)
   content = downloader.get_file_content('my-volume', 'my_new_file_name.txt')

The difference between these two downloaders is that SXFileCat streams files
block-by-block from SX Cluster and thus is memory, disk and network efficient
but not time efficient.

On the contrary, SXFileDownloader streams every file to a temporary file and
then yields the content of that file. This is done on multiple threads and
connections, therefore it is time efficient but neither memory nor disk, nor
network efficient.

SXFileCat in the example isn't used as a context manager since there is no need
to initialize and clean its context. You can still use it with the ``with``
statement though.


Additional documentation
------------------------

For more information regarding usage of a specific object see its docstring.
For example, to see the description of ``listVolumes``, use Python built-in
``help`` function (note that the first letter is capitalized)::

   >>> help(sxclient.operations.ListVolumes)

or run ``pydoc`` in your favourite shell::
   
   $ pydoc sxclient.operations.ListVolumes

Alternatively, in case you have already initialized an SXController object in
the interpreter, you can use a shortcut::

   >>> help(sx.listVolumes)
