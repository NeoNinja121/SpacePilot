import * as React from "react";
import { GameEvent } from "@/types/game";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface EventDisplayProps {
  event: GameEvent;
  onRespond: (isYes: boolean) => void;
  smallDisplay?: boolean;
}

const EventDisplay: React.FC<EventDisplayProps> = ({ 
  event, 
  onRespond,
  smallDisplay = false 
}) => {
  // Animation state
  const [isVisible, setIsVisible] = React.useState(false);
  
  React.useEffect(() => {
    // Animate in
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 100);
    
    return () => clearTimeout(timer);
  }, []);

  // Map event type to styling
  const getEventTypeStyle = () => {
    switch (event.type) {
      case "everyday":
        return "border-blue-500";
      case "rare":
        return "border-purple-500";
      case "cosmic":
        return "border-green-500";
      case "easter_egg":
        return "border-yellow-500";
      default:
        return "border-gray-500";
    }
  };

  // Truncate or simplify event text for small displays
  const getTruncatedDescription = (text: string, maxLength: number = 120) => {
    if (!text) return "";
    if (text.length <= maxLength) return text;
    
    // Try to find a sentence break near the maxLength
    const lastSentence = text.substring(0, maxLength).lastIndexOf('.');
    if (lastSentence > maxLength * 0.6) {
      return text.substring(0, lastSentence + 1);
    }
    
    // Otherwise, truncate at word boundary
    return text.substring(0, maxLength).replace(/\s\S*$/, '...');
  };

  return (
    <div 
      className={cn(
        "fixed inset-0 flex items-center justify-center bg-black/80 z-50 transition-opacity duration-300",
        isVisible ? "opacity-100" : "opacity-0"
      )}
    >
      <Card 
        className={cn(
          "bg-black border-2 overflow-auto",
          smallDisplay ? "w-[90%] max-h-[80%]" : "w-5/6 max-w-md max-h-[80vh]",
          getEventTypeStyle()
        )}
      >
        <CardHeader className={smallDisplay ? "p-2" : ""}>
          <CardTitle className={cn(
            "text-center text-green-400",
            smallDisplay ? "text-sm" : ""
          )}>
            {event.title}
          </CardTitle>
        </CardHeader>
        <CardContent className={cn(
          "text-green-300",
          smallDisplay ? "p-2 space-y-1" : "px-4 py-2"
        )}>
          <p className={cn(
            "leading-relaxed",
            smallDisplay ? "text-xs mb-1" : "text-sm mb-4"
          )}>
            {smallDisplay 
              ? getTruncatedDescription(event.description, 80) 
              : event.description
            }
          </p>
          
          {event.options && event.options.length > 0 && (
            <div className={smallDisplay ? "mt-1 space-y-1" : "mt-4 space-y-2"}>
              <div className={cn(
                "border border-green-700 rounded bg-black/50",
                smallDisplay ? "p-1" : "p-2"
              )}>
                <p className={cn(
                  "text-green-400",
                  smallDisplay ? "text-[10px]" : "text-xs"
                )}>
                  {event.options[0].text}
                </p>
                {!smallDisplay && (
                  <p className="text-xs text-green-600">{event.options[0].effect}</p>
                )}
              </div>
              
              {event.options.length > 1 && (
                <div className={cn(
                  "border border-green-700 rounded bg-black/50",
                  smallDisplay ? "p-1" : "p-2"
                )}>
                  <p className={cn(
                    "text-green-400",
                    smallDisplay ? "text-[10px]" : "text-xs"
                  )}>
                    {event.options[1].text}
                  </p>
                  {!smallDisplay && (
                    <p className="text-xs text-green-600">{event.options[1].effect}</p>
                  )}
                </div>
              )}
            </div>
          )}
        </CardContent>
        <CardFooter className={smallDisplay ? "p-2 pb-3" : "px-6 py-3"}>
          <div className="grid grid-cols-2 gap-2 w-full">
            <Button 
              variant="outline" 
              className={cn(
                "border-green-600 text-green-400 bg-black hover:bg-green-900",
                smallDisplay ? "text-xs py-1 h-8" : "w-24"
              )}
              onClick={() => onRespond(true)}
            >
              {smallDisplay ? "Yes" : "Yes (3)"}
            </Button>
            <Button 
              variant="outline" 
              className={cn(
                "border-green-600 text-green-400 bg-black hover:bg-green-900",
                smallDisplay ? "text-xs py-1 h-8" : "w-24"
              )}
              onClick={() => onRespond(false)}
            >
              {smallDisplay ? "No" : "No (4)"}
            </Button>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
};

export default EventDisplay;
