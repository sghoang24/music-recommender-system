import useDebounce from 'hooks/useDebounce'
import React, { useEffect, useState } from 'react'
import qs from 'query-string'
import Input from './Input'
import { useNavigate } from 'react-router-dom'

const SearchInput = () => {
    const [value, setValue] = useState("") 
    const debouncedValue = useDebounce(value, 500)
    const navigate = useNavigate()

    useEffect(() => {
        const query = {
            title : debouncedValue
        }

        const url = qs.stringifyUrl({
            url : '/search',
            query: query
        })
        navigate(url)
    }, [debouncedValue, navigate])
  return (
    <Input placeholder="Search for songs" value={value} onChange={(e) => setValue(e.target.value)}/>
  )
}

export default SearchInput