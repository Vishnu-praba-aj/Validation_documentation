

export const metadataKeyMap: Record<string, string> = {
  'start-index-nbr': 'StartIndex',
  'end-index-nbr': 'EndIndex',
  'row_adder-cnt': 'RowAdderCount',
  'Col_Adder_CNT': 'ColumnAdderCount',
  'PARAM_Rref_Delim_txt': 'ParamRefDelimiter',
  'Param_value_pos_cd': 'ParamValuePositionCode',
  'Unit_price_pct_ind': 'UnitPricePercentIndicator',
  'Param_nm_occur_ind': 'ParamOccurrenceIndicator',
  'Date_format_cd': 'DateFormatCode',
  'Decimal_seperator_cd': 'DecimalSeparatorCode',
  'Param_def_value_txt': 'ParamDefaultValue',
  'Derivation_col': 'DerivationColumn',
  'Operations_seq': 'OperationsSequence',
  'Param_val_fn_txt': 'ParamValueText'
};



export function mapMetadataKeys(
  metadata: Record<string, any>,
  keyMap: Record<string, string> = metadataKeyMap
): Record<string, any> {
  const newMetadata: Record<string, any> = {};
  for (const key in metadata) {
    const newKey = keyMap[key] || key;
    newMetadata[newKey] = metadata[key];
  }
  return newMetadata;
}
