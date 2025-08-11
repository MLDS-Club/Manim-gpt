import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";

export default function Home() {
  const fetchVideo = async () => {
    try {
      // need to change the api url accordingly
      const response = await fetch(`http://localhost:3000/generatevideo`);
      const todos = await response.json();
    } catch (error) {
      console.error("Error fetching todos:", error);
    }
  };

  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <h1>MANIMGPT.</h1>
        <div className="flex flex-row gap-2.5 w-full">
          <div className="w-150">
            <Textarea
              className="w-full resize-none"
              placeholder="What problems would you like me to visually explain?"
            />
          </div>
          <Button className="w-12 h-12 shrink-0" variant="outline">
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </main>
    </div>
  );
}
