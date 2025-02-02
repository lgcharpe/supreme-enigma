import { useLoaderData } from "react-router";
import { useState } from "react";
import { format } from "date-fns";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
  Button,
  Calendar,
  Popover,
  PopoverContent,
  PopoverTrigger,
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "~/components/ui";
import { Calendar as CalendarIcon, Loader2 } from "lucide-react";
import type { DateRange } from "react-day-picker";

export async function loader({ request }: { request: Request }) {
  const url = new URL(request.url);
  const country = url.searchParams.get("country") || "no";
  const topic = url.searchParams.get("topic");
  const dateFrom = url.searchParams.get("dateFrom");
  const dateTo = url.searchParams.get("dateTo");

  const [topics, summaryData] = await Promise.all([
    fetch(`http://localhost:8000/topics/${country}`).then((r) => r.json()),
    (async () => {
      let summaryUrl = `http://localhost:8000/summary/${country}`;

      if (dateFrom) {
        if (dateTo) {
          summaryUrl += `/period/${dateFrom}/${dateTo}`;
        } else {
          summaryUrl += `/date/${dateFrom}`;
        }
      } else {
        summaryUrl += "/latest";
      }

      if (topic) {
        summaryUrl += `/${topic}`;
      }

      return fetch(summaryUrl).then((r) => r.json());
    })(),
  ]);

  return {
    topics,
    summaryData: summaryData.meta_summary || summaryData.responses[0].response,
    defaultCountry: country,
    selectedTopic: topic || undefined,
    dateRange: dateFrom
      ? {
          from: new Date(dateFrom),
          to: dateTo ? new Date(dateTo) : undefined,
        }
      : undefined,
  };
}

const COUNTRIES = [
  { code: "no", name: "Norway", flag: "🇳🇴" },
  { code: "se", name: "Sweden", flag: "🇸🇪" },
  { code: "dk", name: "Denmark", flag: "🇩🇰" },
];

export default function Index() {
  const {
    topics = [],
    summaryData = {},
    defaultCountry = "no",
    selectedTopic: initialTopic,
    dateRange: initialDateRange,
  } = useLoaderData<typeof loader>();

  const [dateRange, setDateRange] = useState<DateRange | undefined>(
    initialDateRange,
  );
  const [selectedCountry, setSelectedCountry] = useState(defaultCountry);
  const [selectedTopic, setSelectedTopic] = useState<string | undefined>(
    initialTopic,
  );
  const [isLoading, setIsLoading] = useState(false);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsLoading(true);

    const searchParams = new URLSearchParams();
    searchParams.set("country", selectedCountry);

    if (selectedTopic) {
      searchParams.set("topic", selectedTopic);
    }

    if (dateRange?.from) {
      searchParams.set("dateFrom", format(dateRange.from, "yyyy-MM-dd"));
      if (dateRange.to) {
        searchParams.set("dateTo", format(dateRange.to, "yyyy-MM-dd"));
      }
    }

    window.location.search = searchParams.toString();
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 mt-24">
      <h1 className="text-4xl font-bold text-center mb-8">DemocracyUpdate</h1>

      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center gap-4"
      >
        <div className="flex gap-4 justify-center">
          <Select
            defaultValue={defaultCountry}
            onValueChange={setSelectedCountry}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Country" />
            </SelectTrigger>
            <SelectContent>
              {COUNTRIES.map((country) => (
                <SelectItem key={country.code} value={country.code}>
                  <span className="flex items-center gap-2">
                    <span>{country.flag}</span>
                    <span>{country.name}</span>
                  </span>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Select defaultValue="no">
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Language" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="no">Norwegian</SelectItem>
              <SelectItem value="sv">Swedish</SelectItem>
              <SelectItem value="da">Danish</SelectItem>
              <SelectItem value="en">English</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="w-fit">
          <Select value={selectedTopic} onValueChange={setSelectedTopic}>
            <SelectTrigger className="w-[300px]">
              <SelectValue placeholder="Anything you care about in particular?" />
            </SelectTrigger>
            <SelectContent>
              {(topics || []).map((topic) => (
                <SelectItem key={topic?.id} value={topic?.id}>
                  {topic?.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="w-fit">
          <Popover>
            <PopoverTrigger asChild>
              <Button variant="outline" className="w-[300px]">
                <CalendarIcon className="mr-2 h-4 w-4" />
                {dateRange?.from ? (
                  dateRange.to ? (
                    <>
                      {format(dateRange.from, "LLL dd, y")} -{" "}
                      {format(dateRange.to, "LLL dd, y")}
                    </>
                  ) : (
                    format(dateRange.from, "LLL dd, y")
                  )
                ) : (
                  <span>Pick a date range</span>
                )}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0">
              <Calendar
                initialFocus
                mode="range"
                selected={dateRange}
                onSelect={setDateRange}
                numberOfMonths={2}
              />
            </PopoverContent>
          </Popover>
        </div>

        <Button type="submit" className="mt-4" disabled={isLoading}>
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Loading...
            </>
          ) : (
            "Get Summary"
          )}
        </Button>
      </form>

      <div className="mt-8 mb-4 text-2xl font-semibold text-center">
        {dateRange?.from ? (
          dateRange.to ? (
            <>
              Summary of {format(dateRange.from, "LLL dd, y")} -{" "}
              {format(dateRange.to, "LLL dd, y")}
            </>
          ) : (
            <>Summary of {format(dateRange.from, "LLL dd, y")}</>
          )
        ) : (
          <>Summary of Last Two Weeks</>
        )}
      </div>

      {console.log(summaryData)}

      <div className="mt-8">
        <Accordion type="single" collapsible>
          <AccordionItem value="summary">
            <AccordionTrigger>Summary</AccordionTrigger>
            <AccordionContent>
              {summaryData?.summary || "No summary available"}
            </AccordionContent>
          </AccordionItem>

          {/* Period Summary specific sections */}
          {"keyPoliticians" in summaryData && (
            <>
              <AccordionItem value="politicians">
                <AccordionTrigger>Key Politicians</AccordionTrigger>
                <AccordionContent>
                  {summaryData.keyPoliticians?.map((p, i) => (
                    <div key={i} className="mb-4">
                      <h4 className="font-bold">
                        {p.name} ({p.party})
                      </h4>
                      <ul className="list-disc pl-4">
                        {p.mainArguments?.map((arg, j) => (
                          <li key={j}>{arg}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="disputes">
                <AccordionTrigger>Disputes</AccordionTrigger>
                <AccordionContent>
                  {summaryData.disputes?.map((dispute, i) => (
                    <div key={i} className="mb-4">
                      <h4 className="font-bold">{dispute.topic}</h4>
                      <p className="text-sm text-gray-600">
                        Parties: {dispute.parties.join(", ")}
                      </p>
                      <p>{dispute.summary}</p>
                    </div>
                  ))}
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="agreements">
                <AccordionTrigger>Agreements</AccordionTrigger>
                <AccordionContent>
                  {summaryData.agreements?.map((agreement, i) => (
                    <div key={i} className="mb-4">
                      <h4 className="font-bold">{agreement.topic}</h4>
                      <p className="text-sm text-gray-600">
                        Parties: {agreement.parties.join(", ")}
                      </p>
                      <p>{agreement.summary}</p>
                    </div>
                  ))}
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="voting">
                <AccordionTrigger>Voting Results</AccordionTrigger>
                <AccordionContent>
                  {summaryData.votingResults?.map((vote, i) => (
                    <div key={i} className="mb-4">
                      <h4 className="font-bold">{vote.motion}</h4>
                      <p>Result: {vote.result}</p>
                      <p>
                        For: {vote.forCount} | Against: {vote.againstCount}
                      </p>
                    </div>
                  ))}
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="funny">
                <AccordionTrigger>Funny Moments</AccordionTrigger>
                <AccordionContent>
                  {summaryData.funnyMoments?.map((moment, i) => (
                    <div key={i} className="mb-4">
                      <p>{moment.description}</p>
                      <p className="text-sm text-gray-600">
                        Involving: {moment.politicians.join(", ")}
                      </p>
                    </div>
                  ))}
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="special">
                <AccordionTrigger>Special Events</AccordionTrigger>
                <AccordionContent>
                  {summaryData.specialEvents?.map((event, i) => (
                    <div key={i} className="mb-4">
                      <h4 className="font-bold">{event.type}</h4>
                      <p>{event.description}</p>
                      <p className="text-sm text-gray-600">
                        Impact: {event.impact}
                      </p>
                    </div>
                  ))}
                </AccordionContent>
              </AccordionItem>
            </>
          )}

          {/* Topic Summary specific sections */}
          {"keyDecisions" in summaryData && (
            <>
              <AccordionItem value="decisions">
                <AccordionTrigger>Key Decisions</AccordionTrigger>
                <AccordionContent>
                  {summaryData.keyDecisions?.map((decision, i) => (
                    <div key={i} className="mb-4">
                      <h4 className="font-bold">{decision.date}</h4>
                      <p>{decision.description}</p>
                      <p className="text-sm text-gray-600">
                        Impact: {decision.impact}
                      </p>
                    </div>
                  ))}
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="status">
                <AccordionTrigger>Current Status</AccordionTrigger>
                <AccordionContent>
                  <p>{summaryData.currentStatus?.state}</p>
                  <p className="text-sm text-gray-600">
                    Last Updated: {summaryData.currentStatus?.lastUpdated}
                  </p>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="nextsteps">
                <AccordionTrigger>Next Steps</AccordionTrigger>
                <AccordionContent>
                  {summaryData.nextSteps?.map((step, i) => (
                    <div key={i} className="mb-4">
                      <p>{step.description}</p>
                      <p className="text-sm text-gray-600">
                        Expected: {step.expectedDate}
                      </p>
                    </div>
                  ))}
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="feedback">
                <AccordionTrigger>Public Feedback</AccordionTrigger>
                <AccordionContent>
                  <p className="mb-2">{summaryData.publicFeedback?.summary}</p>
                  <h4 className="font-bold mb-2">Main Concerns:</h4>
                  <ul className="list-disc pl-4">
                    {summaryData.publicFeedback?.mainConcerns.map(
                      (concern, i) => <li key={i}>{concern}</li>,
                    )}
                  </ul>
                </AccordionContent>
              </AccordionItem>
            </>
          )}
        </Accordion>
      </div>
    </div>
  );
}
