import * as React from "react"
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd"
import { Card } from "../components/ui/card"
import { Helmet } from "react-helmet-async"
import { useToast } from "../components/ui/use-toast"
import { useTranslation } from "react-i18next"

interface Activity {
  id: string
  title: string
  location: string
  duration: string
}

interface DayPlan {
  id: string
  date: string
  activities: Activity[]
}

const mockActivities: Activity[] = [
  { id: "1", title: "Visit Tanah Lot Temple", location: "Bali", duration: "3 hours" },
  { id: "2", title: "Surf at Kuta Beach", location: "Bali", duration: "2 hours" },
  { id: "3", title: "Explore Ubud Rice Terraces", location: "Bali", duration: "4 hours" },
  { id: "4", title: "Visit MONAS", location: "Jakarta", duration: "2 hours" },
  { id: "5", title: "Shop at Grand Indonesia", location: "Jakarta", duration: "3 hours" },
]

export default function Plans() {
  const { t } = useTranslation()
  const { toast } = useToast()
  const [days, setDays] = React.useState<DayPlan[]>([
    { id: "day-1", date: "Day 1", activities: [] },
    { id: "day-2", date: "Day 2", activities: [] },
    { id: "day-3", date: "Day 3", activities: [] },
  ])
  const [availableActivities] = React.useState<Activity[]>(mockActivities)

  const onDragEnd = (result: { source: { droppableId: string; index: number }; destination?: { droppableId: string; index: number }; draggableId: string }) => {
    const { source, destination } = result

    if (!destination) return

    if (source.droppableId === "activities" && destination.droppableId !== "activities") {
      // Moving from available activities to a day
      const activity = availableActivities[source.index]
      const updatedDays = days.map(day => {
        if (day.id === destination.droppableId) {
          return {
            ...day,
            activities: [...day.activities, activity]
          }
        }
        return day
      })
      setDays(updatedDays)
      toast({
        title: t('plans.activityAdded', { day: destination.droppableId }),
        description: activity.title,
      })
    } else if (source.droppableId !== "activities" && destination.droppableId !== "activities") {
      // Reordering within a day or moving between days
      const sourceDay = days.find(d => d.id === source.droppableId)
      const destDay = days.find(d => d.id === destination.droppableId)
      
      if (sourceDay && destDay) {
        const newDays = days.map(day => {
          if (day.id === sourceDay.id) {
            return {
              ...day,
              activities: day.activities.filter((_, index) => index !== source.index)
            }
          }
          if (day.id === destDay.id) {
            const newActivities = [...day.activities]
            newActivities.splice(destination.index, 0, sourceDay.activities[source.index])
            return {
              ...day,
              activities: newActivities
            }
          }
          return day
        })
        setDays(newDays)
      }
    }
  }


  return (
    <>
      <Helmet>
        <title>{t('plans.title')} | Cemelin Travel</title>
        <meta name="description" content={t('plans.description')} />
      </Helmet>

      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">{t('tripPlanning')}</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Available Activities */}
          <div className="lg:col-span-1">
            <Card className="p-4">
              <h2 className="text-xl font-semibold mb-4 text-gray-900">{t('plans.availableActivities')}</h2>
              <p className="text-sm text-gray-600 mb-4">{t('plans.dragActivities')}</p>
              <DragDropContext onDragEnd={onDragEnd}>
                <Droppable droppableId="activities">
                  {(provided) => (
                    <div
                      {...provided.droppableProps}
                      ref={provided.innerRef}
                      className="space-y-2 transition-all duration-300"
                    >
                      {availableActivities.map((activity, index) => (
                        <Draggable
                          key={activity.id}
                          draggableId={activity.id}
                          index={index}
                        >
                          {(provided) => (
                            <div
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              className="p-3 bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-all duration-300 hover:scale-102 hover:border-blue-200 transform"
                            >
                              <h3 className="font-medium">{activity.title}</h3>
                              <p className="text-sm text-gray-600">{activity.location} • {activity.duration}</p>
                            </div>
                          )}
                        </Draggable>
                      ))}
                      {provided.placeholder}
                    </div>
                  )}
                </Droppable>
              </DragDropContext>
            </Card>
          </div>

          {/* Days */}
          <div className="lg:col-span-3">
            <DragDropContext onDragEnd={onDragEnd}>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {days.map((day) => (
                  <Card key={day.id} className="p-4">
                    <h2 className="text-xl font-semibold mb-4 text-gray-900">{t('plans.day', { number: day.date.split(' ')[1] })}</h2>
                    <Droppable droppableId={day.id}>
                      {(provided) => (
                        <div
                          {...provided.droppableProps}
                          ref={provided.innerRef}
                          className="min-h-[200px] space-y-2 transition-all duration-300"
                        >
                          {day.activities.map((activity, index) => (
                            <Draggable
                              key={activity.id}
                              draggableId={`${day.id}-${activity.id}`}
                              index={index}
                            >
                              {(provided) => (
                                <div
                                  ref={provided.innerRef}
                                  {...provided.draggableProps}
                                  {...provided.dragHandleProps}
                                  className="p-3 bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-all duration-300 hover:scale-102 hover:border-blue-200 transform"
                                >
                                  <h3 className="font-medium">{activity.title}</h3>
                                  <p className="text-sm text-gray-600">{activity.duration}</p>
                                </div>
                              )}
                            </Draggable>
                          ))}
                          {provided.placeholder}
                        </div>
                      )}
                    </Droppable>
                  </Card>
                ))}
              </div>
            </DragDropContext>
          </div>
        </div>
      </div>
    </>
  )
}
