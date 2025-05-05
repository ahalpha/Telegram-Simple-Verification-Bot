async def link_md( link ):
    
    link = link.replace("+", "\+")

    link = link.replace("-", "\-")

    link = link.replace(".", "\.")

    return link