local pandoc = require("pandoc")
local revisiones_block = {}

function Meta(meta)
  if meta.revisiones then
    for _, rev in ipairs(meta.revisiones) do
      local fecha = pandoc.utils.stringify(rev.fecha)
      local desc = pandoc.utils.stringify(rev.descripcion)
      local autor = pandoc.utils.stringify(rev.autor)

      table.insert(revisiones_block, pandoc.Para({
        pandoc.Str(fecha .. ": " .. desc .. " – " .. autor)
      }))
    end
  end
  return meta
end

function RawBlock(el)
  if el.format == "markdown" and el.text == "[[REVISIONS]]" then
    return revisiones_block
  end
end

--- Filter function; this is the entrypoint when used as a filter.
function Pandoc(doc)
  -- Check if the document has a metadata field named "revisiones"
  if doc.meta.revisiones then
    -- If it does, process the revisions and return the modified document
    return doc:walk {
      RawBlock = RawBlock,
      Meta = Meta      
    }
  end
  -- If not, return the document unchanged
  return doc
end
