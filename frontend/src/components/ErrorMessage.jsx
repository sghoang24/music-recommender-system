import React from 'react'

const ErrorMessage = ({message}) => {
  return (
    <>
        {message==="User created successfully" ? (
            <div className='w-full bg-green-500 p-4 flex gap-x-3 mb-3'>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                </svg>

                <p>
                    {message}
                </p>
            </div>

        ) : (message) ? (
            <div className='w-full bg-red-600 p-4 flex gap-x-3 mb-3'>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
                </svg>
                <p>
                    {message}
                </p>
            </div>
        ) : (
            <></>
        )}
    </>
  )
}

export default ErrorMessage