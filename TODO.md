# todo

- sneaky url should maintain current week
- don't pass raw user-name in URL for PUT/DELETE
  - seems to be breaking if name contains forward slash `/`
  - quick fix: sanitize/format, or just prevent with js
  - long-term fix: either use body or introduce user_id
- explicitly support the future
  - current week is actually current week, no special behavior for sat/sun
    - instead, only show link to next week if sat/sun
  - email urls include explicit link to the week
  - "Looking for last week or next week?"
- add way of choosing/highlighting a date (secret input like keyboard + mouse?)
- add hard-coded, event-type-specific times
- add instructions to email
- add free-edit text subtitle to each event for customization?
- move combined file store to one file per event-week?
