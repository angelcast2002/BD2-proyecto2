import { useState, useEffect } from "react"

function useIsImage() {
  const getFileTypeFromBase64 = (base64String) => {
    const typeMatch = base64String.match(/^data:(.+);base64,/)

    if (typeMatch) {
      return typeMatch[1]
    }

    return null
  }

  const isImage = (image) => {
    const fileType = getFileTypeFromBase64(image)
    return fileType && fileType.startsWith("image/")
  }

  return isImage
}

export default useIsImage
