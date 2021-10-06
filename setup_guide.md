# How to set up an automated CLI checkin
_This guide is meant for MacOS and has been checked to work on MacOS 10.15._

## Make a checkin script
You can test this in your Terminal until you're satisfied. Simple example:
```python
print("Time for a quick checkin!")
answers = []
for q in ["any blockers so far today?", "anything else?"]:
    answers.append(input(f"{q}\n"))
with open("answers.tsv", "a") as f:
    f.write("\t".join(answers))
print("Thank you :-)")
```
Save this script, it'll be run automatically in a scheduled way later.

## In Automator:
- File > New > Application
- add "Run AppleScript" action
- write your script, for example:
  ```applescript
on run {input, parameters}
	-- open terminal
	tell application "Terminal"
		-- open new window only if not present
		if not (exists window 1) then reopen
		activate

		-- run the CLI script, then close Terminal
		do script "cd ~/Documents/self-checkins; python run.py; exit" in window 1
		
		-- quit Terminal once closed
		repeat until not (exists window 1)
			delay 1
		end repeat
		quit
	end tell
	return input
end run
  
  ```
- save as `<name>.app` in some folder

## In iCal:
- Create new event
- double click to edit properties
- set repeating frequency
- under "alert" choose Custom > Open file > choose the `<name>.app` created in Automator
