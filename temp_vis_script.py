import pandas as pd

from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/chinook.db")

connection = engine.connect()

result_df = pd.read_sql("SELECT ar.Name AS Artist, COUNT(ii.TrackId) AS TracksSold FROM invoice_items ii JOIN tracks t ON ii.TrackId = t.TrackId JOIN albums al ON t.AlbumId = al.AlbumId JOIN artists ar ON al.ArtistId = ar.ArtistId JOIN invoices i ON ii.InvoiceId = i.InvoiceId WHERE strftime('%Y', i.InvoiceDate) = '2013' GROUP BY ar.Name ORDER BY TracksSold DESC LIMIT 10;", connection)

connection.close()


st.bar_chart(data=result_df, x='Artist', y='TracksSold')

