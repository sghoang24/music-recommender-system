import React, { useMemo } from 'react'
import {useLocation} from 'react-router-dom'
import {HiHome} from 'react-icons/hi' 
import {BiSearch} from 'react-icons/bi'
import Box from './Box'
import SidebarItem from './SidebarItem'
import Library from './Library'
import usePlayer from 'hooks/usePlayer'
import { twMerge } from 'tailwind-merge'

const Sidebar = ({children}) => {
    const {pathname} = useLocation()
    const player = usePlayer()
    
    const routes = useMemo(() => [
        {
            icon : HiHome,
            label : 'Home',
            active : pathname === '/',
            href : '/'
        },
        {
            icon : BiSearch,
            label : 'Search', 
            active : pathname === '/search',
            href : '/search'
        }
    ], [pathname])
  return (
    <div className="flex h-full" >
        <div className={twMerge(`
            hidden md:flex flex-col gap-y-2 bg-black max-h-full h-[100vh] w-full max-w-[300px] p-2
        `, player.activeId && "h-[calc(100vh-72px)]")}>

            <Box className="h-1/4">
                <div className='flex flex-col gap-y-4 px-5 py-4'>
                    {routes.map((item) => (
                        <SidebarItem 
                            key={item.label}
                            {...item}
                        />
                    ))}

                </div>
            </Box>

            <Box className="overflow-y-auto h-screen">
                <Library />
            </Box>
        </div>
        
        <div className='h-full max-h-full w-full overflow-y-auto'>
            <main className='flex-grow py-2'>
                {children}
            </main>
        </div>
    </div>
  )
}

export default Sidebar