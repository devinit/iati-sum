list.of.packages <- c("data.table","readr","varhandle","reshape2")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)
lapply(list.of.packages, require, character.only=T)

wd = "~/git/iati-sum"
setwd(wd)

pubs = read.csv("pubs.csv",na.strings="",as.is=T)

dat = read_csv("iati.csv",col_types = cols(.default = "c"))
if(is.factor(dat$year)){
  dat$year = unfactor(dat$year)
}
if(is.factor(dat$usd_value)){
  dat$usd_value = unfactor(dat$usd_value)
}
dat$year = as.numeric(dat$year)
dat$usd_value = as.numeric(dat$usd_value)

dat = merge(dat,pubs,by="publisher_id")

partners = read.csv("development_partners.csv", na.strings="",as.is=T)$publisher_name

dat = subset(dat, publisher_name %in% partners)

dat = data.table(dat)
dat_activity = dat[,.(sum=sum(usd_value,na.rm=T)),by=.(publisher_id,publisher_name,iati_identifier, reporting_org_id, reporting_org_name, year)]

dat_activity.m = melt(dat_activity, id.vars=c("publisher_id", "publisher_name", "iati_identifier", "reporting_org_id", "reporting_org_name", "year"))
dat_activity.w = dcast(dat_activity.m,publisher_id+publisher_name+iati_identifier+reporting_org_id+reporting_org_name~variable+year)

write.csv(dat_activity.w, "results_activity.csv", na="", row.names=F)

dat_master = dat[,.(sum=sum(usd_value,na.rm=T)),by=.(publisher_id, publisher_name,reporting_org_id, reporting_org_name, year)]

dat_master.m = melt(dat_master, id.vars=c("publisher_id", "publisher_name", "reporting_org_id", "reporting_org_name", "year"))
dat_master.w = dcast(dat_master.m,publisher_id+publisher_name+reporting_org_id+reporting_org_name~variable+year)

write.csv(dat_master.w, "results_master.csv", na="", row.names=F)

missing_partners = data.frame(missing_partner = partners[!(partners %in% dat$publisher_name)])
write.csv(missing_partners,"missing_partners.csv",row.names=F,na="")
