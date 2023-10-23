library(tidyverse)
library(tidygeocoder)

home_directory <- path.expand("~")
in_file <- file.path(home_directory, "apple_us_store_address.csv")
apple_us_store_addresses <- read_csv(in_file)

lat_longs <- geocode(
  apple_us_store_addresses, 
  address, 
  method = 'osm', 
  lat = latitude , 
  long = longitude
  )

out_file <- file.path(home_directory, "apple_store_us_locations.csv")
write_csv(lat_longs, out_file)
