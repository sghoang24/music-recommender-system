import { useState } from 'react'
import MediaItem from './MediaItem'
import LikeButton from './LikeButton'
import { IoIosArrowUp, IoIosArrowDown } from 'react-icons/io'
import { Card, CardBody, Collapse, Typography } from '@material-tailwind/react'

const ListRowItem = ({
    song,
    onClick
}) => {
    const [showCollapsible, setShowCollapsible] = useState(false)

    const toggleCollapsible = () => {
        setShowCollapsible(!showCollapsible)
    }
  return (
    <div>
        <div key={song.id} className='flex items-center gap-x-4 w-full'>
            <div className='flex-1'>
                <MediaItem onClick={onClick} data={song}/>
            </div>
            <LikeButton songId={song.id}/>
            {showCollapsible ? (
                <IoIosArrowUp onClick={toggleCollapsible}/>
            ) : (
                <IoIosArrowDown onClick={toggleCollapsible}/>
            )}
        </div>
        <Collapse open={showCollapsible}>
            <Card className='my-4 mx-auto w-full text-white rounded-md bg-neutral-700'>
                <CardBody>
                    <Typography>
                        Mutual tags : 
                        {song.tags.split(", ").map((tag) => (
                            <span className='text-blue-300'> #{tag} </span>
                        ))}
                    </Typography>
                </CardBody>
            </Card>
        </Collapse>
    </div>
  )
}

export default ListRowItem