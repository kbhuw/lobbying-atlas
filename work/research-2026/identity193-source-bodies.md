# identity193 primary-source body captures (follow-up)

These are the exact body excerpts returned by the web fetches in this follow-up. The `turn...` references are the tool response IDs; URLs are preserved so the evidence can be re-fetched.

## DailyPay — `12ee893e54bc5fb3`

URL: https://www.dailypay.com/en-us/legal/terms-of-service/

Tool response: `turn7732view0`, lines 131–137.

> Last updated: March 30, 2026
>
> Welcome to DailyPay! DailyPay, LLC (“DailyPay,” “our,” “us” or “we”) provides employers with access to a platform that enables employees and other service providers to access On-Demand Pay and Frontline Communications...
>
> These Terms ... govern ... our website, www.dailypay.com ... (together, the “Site”), our mobile applications ... and ... the “Services”.

Decision: this is a direct legal-name/domain bridge, but it establishes **DailyPay, LLC**, not the reviewed label “DailyPay Inc.” Keep the record partial until the LDA client is reconciled to the LLC entity (or the reviewed name is corrected). Ownership remains unknown.

## Ventura Water — `3c9ec24d9689fc1b`

URL: https://www.cityofventura.ca.gov/

Tool response: `turn7726view0`, lines 120–129 and 113–115.

> ### Contact Us
>
> City of Ventura
> 501 Poli Street
> Ventura, CA 93001
> Phone: 805-654-7800
> City Department Directory
>
> Ventura Water Billing

Decision: confirms the current municipal parent and that Ventura Water is a city service. It does not print the exact formal phrase “Department of the City of San Buenaventura”; retain the municipal identity, but keep the exact legal-name bridge as a gap rather than upgrading on this page alone.

## Datamaxx — `686b08ce58e62dc0`

URL: https://www.datamaxx.com/Info/About?AspxAutoDetectCookieSupport=1

Tool response: `turn7728search1` (official Datamaxx About page body returned by the search fetch; direct root fetch separately returned an internal error).

> ### Company Overview
>
> Datamaxx, headquartered in Tallahassee, Fla., is the premier provider of advanced communications, data access, information sharing, enterprise intelligence, and access control solutions to the law enforcement, criminal justice, public safety, and security industries. Datamaxx is a privately held, Florida-certified and woman-owned enterprise...
>
> ### Company History
>
> 1991 | Datamaxx Applied Technologies, Inc., formed as a Florida-certified, woman-owned business

Decision: exact legal name and “privately held” status are both explicitly supported by the official About body. This record may be promoted to confirmed identity/private company; the direct-root fetch limitation should remain noted.
