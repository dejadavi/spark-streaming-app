from pyspark.sql.types import *

SubScoreSchema = FloatType()

CpeNameSchema = StructType([StructField("cpe23Uri", StringType(), False),
                            StructField("lastModifiedDate", StringType(), True)])


CpeMatchSchema = StructType([StructField("vulnerable", BooleanType(), False),
                             StructField("cpe22Uri", StringType(), True),
                             StructField("cpe23Uri", StringType(), False),
                             StructField("versionStartExcluding", StringType(), True),
                             StructField("versionStartIncluding", StringType(), True),
                             StructField("versionEndExcluding", StringType(), True),
                             StructField("versionEndIncluding", StringType(), True),
                             StructField("cpe_name", ArrayType(CpeNameSchema), True),])

_ChildNodeSchema = StructType([StructField("operator", StringType(), True),
                              StructField("negate", BooleanType(), True),
                              StructField("cpe_match", ArrayType(CpeMatchSchema))])

NodeSchema = StructType([StructField("operator", StringType(), True),
                         StructField("negate", BooleanType(), True),
                         StructField("children", ArrayType(_ChildNodeSchema,True), True),
                         StructField("cpe_match", ArrayType(CpeMatchSchema))])

ConfigurationsSchema = StructType([StructField("CVE_data_version",StringType(), True),
                                   StructField("nodes", ArrayType(NodeSchema)) ])


ImpactSchema = StructType([StructField("baseMetricV2",StructType([StructField("cvssV2", MapType(StringType(),StringType()) ),
                                                      StructField("severity", StringType(),True),
                                                      StructField("exploitabilityScore", SubScoreSchema,True),
                                                      StructField("impactScore", SubScoreSchema,True),
                                                      StructField("acInsufInfo", BooleanType(), True),
                                                      StructField("obtainAllPrivilege", BooleanType(), True),
                                                      StructField("obtainUserPrivilege", BooleanType(), True),
                                                      StructField("obtainOtherPrivilege", BooleanType(), True),
                                                      StructField("userInteractionRequired", BooleanType(), True)])),
                           StructField("baseMetricV3",StructType([StructField("cvssV3", MapType(StringType(),StringType())),
                                                                  StructField("exploitabilityScore", SubScoreSchema,True),
                                                                  StructField("impactScore", SubScoreSchema, True) ]) )])

CveItemSchema = StructType([StructField("cve", StringType(), False),
                            StructField("configurations", ConfigurationsSchema,True),
                            StructField("impact", ImpactSchema,True),
                            StructField("publishedDate", StringType(), True),
                            StructField("lastModifiedDate",  StringType(), True)])

NvdSchema = StructType([StructField("CVE_data_type", StringType(), False),
                        StructField("CVE_data_format", StringType(), False),
                        StructField("CVE_data_version", StringType(), False),
                        StructField("CVE_data_numberOfCVEs", StringType(), False),
                        StructField("CVE_data_timestamp", StringType(), False),
                        StructField("CVE_Items", ArrayType(CveItemSchema, False), False) ])