Welcome to the Python ZaneAPI Wrapper
-------------------------------------
This is a quite simple wrapper for a quite simple API. It's not currently hosted anywhere so the base URL for the API is incorrect; however, the API is open source to combat that.

It can edit an instance of io.BytesIO or you can input a URL to an image for it to have it edited. It always returns io.BytesIO

Example
-------
```python
import zaneapi

client = zaneapi.Client()

# ... in a coro
image_from_bytes = await client.manipulate(
    zaneapi.Operation.Magic,
    image_bytes_io # an io.BytesIO instance containing an image
)   
image_from_url = await client.manipulate(
    zaneapi.Operation.Arc,
    "https://a-ur.l/picture.png"
)

print(type(image_from_url))
# io.BytesIO
```

Discord.py
-

If you are a user of discord.py, this works out quite nicely since you can do the following...

```python
import zaneapi
client = zaneapi.Client()

# ... in a command
# to edit a user's avatar then send the result
image = await client.manipulate(zaneapi.Operation.Magic, str(ctx.author.avatar_url))
await ctx.send(file=discord.File(image, "generated.png"))
```