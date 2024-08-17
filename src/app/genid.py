import secrets
import datetime

def genid() -> str:
	return (
		secrets.token_urlsafe(10)+
		str(
			datetime.datetime
				.now()
				.timestamp()
		)
	)