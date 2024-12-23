import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';
import { Calendar, Clock, MapPin, Trash2 } from 'lucide-react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { toast } from '../ui/use-toast';

interface TripItem {
  id: string;
  place_id: string;
  name: string;
  description: string;
  duration: number;
  day: number;
}

interface TripPlannerProps {
  initialItems?: TripItem[];
  onSave?: (items: TripItem[]) => void;
}

export function TripPlanner({ initialItems = [], onSave }: TripPlannerProps) {
  const { t } = useTranslation();
  const [items, setItems] = useState<TripItem[]>(initialItems);
  const [days, setDays] = useState(Math.max(1, ...initialItems.map(item => item.day)));

  const onDragEnd = (result: any) => {
    if (!result.destination) return;

    const sourceDay = parseInt(result.source.droppableId);
    const destinationDay = parseInt(result.destination.droppableId);
    const sourceIndex = result.source.index;
    const destinationIndex = result.destination.index;

    const newItems = [...items];
    const [removed] = newItems.splice(
      newItems.findIndex(
        item => item.day === sourceDay && item.id === result.draggableId
      ),
      1
    );

    removed.day = destinationDay;
    newItems.splice(
      newItems.findIndex(item => item.day === destinationDay) + destinationIndex,
      0,
      removed
    );

    setItems(newItems);
    if (onSave) onSave(newItems);
  };

  const handleAddDay = () => {
    setDays(days + 1);
  };

  const handleRemoveDay = (day: number) => {
    if (items.some(item => item.day === day)) {
      toast({
        title: t('trips.error'),
        description: t('trips.dayNotEmpty'),
        variant: 'destructive',
      });
      return;
    }
    setDays(days - 1);
    setItems(items.map(item => ({
      ...item,
      day: item.day > day ? item.day - 1 : item.day,
    })));
  };

  const handleRemoveItem = (itemId: string) => {
    setItems(items.filter(item => item.id !== itemId));
    if (onSave) onSave(items.filter(item => item.id !== itemId));
  };

  const handleUpdateDuration = (itemId: string, duration: number) => {
    setItems(items.map(item => 
      item.id === itemId ? { ...item, duration } : item
    ));
    if (onSave) onSave(items.map(item => 
      item.id === itemId ? { ...item, duration } : item
    ));
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-semibold">{t('trips.title')}</h2>
        <Button onClick={handleAddDay}>{t('trips.addDay')}</Button>
      </div>

      <DragDropContext onDragEnd={onDragEnd}>
        <div className="space-y-4">
          {Array.from({ length: days }, (_, i) => i + 1).map(day => (
            <div key={day} className="p-4 bg-white rounded-lg shadow">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium flex items-center">
                  <Calendar className="mr-2 h-5 w-5" />
                  {t('trips.day', { day })}
                </h3>
                {day === days && days > 1 && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleRemoveDay(day)}
                  >
                    {t('trips.removeDay')}
                  </Button>
                )}
              </div>

              <Droppable droppableId={day.toString()}>
                {(provided) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    className="space-y-2"
                  >
                    {items
                      .filter(item => item.day === day)
                      .map((item, index) => (
                        <Draggable
                          key={item.id}
                          draggableId={item.id}
                          index={index}
                        >
                          {(provided) => (
                            <div
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              className="p-3 bg-gray-50 rounded border border-gray-200"
                            >
                              <div className="flex justify-between items-start">
                                <div className="space-y-1">
                                  <div className="font-medium">{item.name}</div>
                                  <div className="text-sm text-gray-500 flex items-center">
                                    <MapPin className="mr-1 h-4 w-4" />
                                    {item.description}
                                  </div>
                                </div>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => handleRemoveItem(item.id)}
                                >
                                  <Trash2 className="h-4 w-4" />
                                </Button>
                              </div>
                              <div className="mt-2 flex items-center space-x-2">
                                <Clock className="h-4 w-4 text-gray-400" />
                                <Input
                                  type="number"
                                  min="0"
                                  value={item.duration}
                                  onChange={(e) => handleUpdateDuration(item.id, parseInt(e.target.value) || 0)}
                                  className="w-20"
                                />
                                <span className="text-sm text-gray-500">
                                  {t('trips.hours')}
                                </span>
                              </div>
                            </div>
                          )}
                        </Draggable>
                      ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            </div>
          ))}
        </div>
      </DragDropContext>
    </div>
  );
}
