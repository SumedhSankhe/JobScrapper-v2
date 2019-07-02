source('D:/Github/mail_function.r')


past_day <- function(dt){
  dt[,dttm := as.POSIXct(dttm, 'EST')]
  dt[, date := as.Date(dttm,'EST')]
  newDT <- dt[date > (Sys.Date() - 1)]
  newDT[,Title := paste0('<a href="',link,'">', Title,"</a>")]
  mailDT <-  newDT[,.(Company, Location, Title, Summary)]
  text <- paste0('Found <b>', nrow(newDT), '</b> new positions, check the table below for something new')
  if (nrow(dt) < 20){
    tempfile <- tempfile(pattern = 'data', fileext = '.csv')
    write.csv(mailDT, tempfile)
  }else{
    tempfile <- NULL
  }
  mail_me(list(text,mailDT), subject = '#Automation: Daily Posts', attachments = tempfile)
  unlink(tempfile)
  return(print('Done'))
}

analysis_fornight <- function(dt){
  dt[,dttm:= as.POSIXct(dttm,'EST')]
  dt[,date:= as.Date(dttm, 'EST')]
  newDT <- dt[date > Sys.Date() - 15]
  anaDT <- newDT[,.N,Company]
  
  mail_me(list(head(anaDT[order(-N)],10)), subject = '#Automation: Fornightly Report')
  
  return(print('Done'))
}

library(data.table)
dt <-  as.data.table(read.csv("D:/Github/JobScrapper-v2/master_data/master.csv", stringsAsFactors = F))
past_day(dt)


